#include "PumpBesselRing.h"
#include "Function.h"
#include <cmath>
#include <numbers>

registerMooseObject("purpleApp", PumpBesselRing);

InputParameters
PumpBesselRing::validParams()
{
  InputParameters params = IntegratedBC::validParams();
  
  params.addClassDescription("Implement a standard gaussian pump laser for the FDTR simulations. Surface must be constant in z.");

  params.addRequiredParam<Real>("pump_power", "Q0, the applied pump power");
  params.addRequiredParam<Real>("absorbance", "The fraction of the pump absorbed by the transducer");
  params.addRequiredParam<Real>("pump_spot_size", "the 1/e^2 beam waist");
  params.addRequiredParam<Real>("offset", "the approximate offset of the pump");
  
  
  params.addRequiredParam<Real>("center_x", "center of the gaussian (x - coordinate)");
  params.addRequiredParam<Real>("center_y", "center of the gaussian (y - coordinate)");
  
  
  
  // params.addClassDescription("Imposes the integrated boundary condition "
                             // "$\\frac{\\partial u}{\\partial n}=h(t,\\vec{x})$, "
                             // "where $h$ is a (possibly) time and space-dependent MOOSE Function.");
							 
  // params.addRequiredParam<FunctionName>("function", "The function.");
  
  return params;
}

PumpBesselRing::PumpBesselRing(const InputParameters & parameters)
  : IntegratedBC(parameters), 
  
    // _func(getFunction("function"))
  
    // Get parameters from user, name in input file is in quotes
	_pump_power(getParam<Real>("pump_power")),
    _absorbance(getParam<Real>("absorbance")),
	_pump_spot_size(getParam<Real>("pump_spot_size")),
	_offset(getParam<Real>("offset")),
	
	_center_x(getParam<Real>("center_x")),
    _center_y(getParam<Real>("center_y"))
  
  
{
}

Real
PumpBesselRing::computeQpResidual()
{
  auto x0 = _center_x;
  auto y0 = _center_y;
  
  auto x = _q_point[_qp](0);
  auto y = _q_point[_qp](1);
  auto z = _q_point[_qp](2);
  
  auto pi = M_PI;
  
  auto Q0 = _pump_power;
  auto absorbance = _absorbance;
  auto w_Pump = _pump_spot_size;
  
  auto x_off = _offset;
  
  auto r_squared = ((std::pow((x-x0), 2.0))+(std::pow((y-y0), 2.0)));
  auto r = std::pow(r_squared, (1.0/2.0));
  
  auto prefactor = ((2*Q0*absorbance)/(pi*(std::pow(w_Pump, 2.0))));
  
  auto exp_term = std::exp(   (- 2.0 * ( r_squared + std::pow(x_off, 2.0)))    /    (std::pow(w_Pump, 2.0))   );
  
  auto bessel_arg = (   (4.0 * x_off * r)    /    (std::pow(w_Pump, 2.0))   );
  auto bessel_term = std::cyl_bessel_i(0.0, bessel_arg);
  
  return -_test[_i][_qp] * (prefactor   *   exp_term  *  bessel_term);
  
  // return -_test[_i][_qp] * _func.value(_t, _q_point[_qp]);
}
