#include "ConcentricGaussianPumpStandardAxisymmetric.h"
#include "Function.h"
#include <cmath>
#include <numbers>

registerMooseObject("purpleApp", ConcentricGaussianPumpStandardAxisymmetric);

InputParameters
ConcentricGaussianPumpStandardAxisymmetric::validParams()
{
  InputParameters params = IntegratedBC::validParams();
  
  params.addClassDescription("Implement a standard gaussian pump laser for the FDTR simulations. Surface must be constant in z.");

  params.addRequiredParam<Real>("pump_power", "Q0, the applied pump power");
  params.addRequiredParam<Real>("absorbance", "The fraction of the pump absorbed by the transducer");
  params.addRequiredParam<Real>("pump_spot_size", "the 1/e beam waist");
  
  
  
  // params.addClassDescription("Imposes the integrated boundary condition "
                             // "$\\frac{\\partial u}{\\partial n}=h(t,\\vec{x})$, "
                             // "where $h$ is a (possibly) time and space-dependent MOOSE Function.");
							 
  // params.addRequiredParam<FunctionName>("function", "The function.");
  
  return params;
}

ConcentricGaussianPumpStandardAxisymmetric::ConcentricGaussianPumpStandardAxisymmetric(const InputParameters & parameters)
  : IntegratedBC(parameters), 
  
    // _func(getFunction("function"))
  
    // Get parameters from user, name in input file is in quotes
	_pump_power(getParam<Real>("pump_power")),
    _absorbance(getParam<Real>("absorbance")),
	_pump_spot_size(getParam<Real>("pump_spot_size"))
  
  
{
}

Real
ConcentricGaussianPumpStandardAxisymmetric::computeQpResidual()
{
  
  auto x = _q_point[_qp](0);
  auto y = _q_point[_qp](1);
  auto z = _q_point[_qp](2);
  
  auto pi = M_PI;
  
  auto Q0 = _pump_power;
  auto absorbance = _absorbance;
  auto w_Pump = _pump_spot_size;
  
  auto prefactor = -((2*Q0*absorbance)/(pi*(std::pow(w_Pump, 2.0))));
  
  auto beam_function = std::exp( (- 2.0 * (std::pow((x), 2.0)) )  /  (std::pow(w_Pump, 2.0)) );
  
  return -_test[_i][_qp] * (prefactor   *   beam_function);
  
  // return -_test[_i][_qp] * _func.value(_t, _q_point[_qp]);
}
