#include "PumpSuperGaussianRingAxisymmetric.h"
#include "Function.h"
#include <cmath>
#include <numbers>

registerMooseObject("purpleApp", PumpSuperGaussianRingAxisymmetric);

InputParameters
PumpSuperGaussianRingAxisymmetric::validParams()
{
  InputParameters params = IntegratedBC::validParams();
  
  params.addClassDescription("Implement a standard gaussian pump laser for the FDTR simulations. Surface must be constant in z.");

  params.addRequiredParam<Real>("pump_power", "Q0, the applied pump power");
  params.addRequiredParam<Real>("absorbance", "The fraction of the pump absorbed by the transducer");
  params.addRequiredParam<Real>("pump_spot_size", "the 1/e^2 beam waist");
  params.addRequiredParam<Real>("offset", "the approximate offset of the pump");
  params.addRequiredParam<Real>("order", "the order of the super gaussian");
  
  
  
  // params.addClassDescription("Imposes the integrated boundary condition "
                             // "$\\frac{\\partial u}{\\partial n}=h(t,\\vec{x})$, "
                             // "where $h$ is a (possibly) time and space-dependent MOOSE Function.");
							 
  // params.addRequiredParam<FunctionName>("function", "The function.");
  
  return params;
}

PumpSuperGaussianRingAxisymmetric::PumpSuperGaussianRingAxisymmetric(const InputParameters & parameters)
  : IntegratedBC(parameters), 
  
    // _func(getFunction("function"))
  
    // Get parameters from user, name in input file is in quotes
	_pump_power(getParam<Real>("pump_power")),
    _absorbance(getParam<Real>("absorbance")),
	_pump_spot_size(getParam<Real>("pump_spot_size")),
	_offset(getParam<Real>("offset")),
	_order(getParam<Real>("order"))
  
  
{
}

Real
PumpSuperGaussianRingAxisymmetric::computeQpResidual()
{
  auto x0 = 0.0;
  
  auto x = _q_point[_qp](0);
  auto y = _q_point[_qp](1);
  auto z = _q_point[_qp](2);
  
  auto pi = M_PI;
  
  auto Q0 = _pump_power;
  auto absorbance = _absorbance;
  auto w_Pump = _pump_spot_size;
  
  auto x_off = _offset;
  
  auto n = _order;
  
  auto r_squared = (std::pow((x-x0), 2.0));
  auto r = std::pow(r_squared, (1.0/2.0));
  
  
  auto exp_term = std::exp(-2.0 * std::pow(((r - x_off) / w_Pump), n));
  
  // Numerically integrate to normalize: ∫[0,∞] exp(-2((r - r0)/w)^n) * 2πr dr
  // Simple trapezoidal rule approximation
  Real integral = 0.0;
  const int N = 10;         // number of steps
  const Real r_max = 10.0 * w_Pump + x_off;  // integration upper bound
  const Real dr = r_max / N;
  
  for (int i = 0; i < N; ++i)
  {
    Real ri = i * dr;
    Real rip1 = (i + 1) * dr;
    
    Real fi = std::exp(-2.0 * std::pow((ri - x_off) / w_Pump, n)) * ri;
    Real fip1 = std::exp(-2.0 * std::pow((rip1 - x_off) / w_Pump, n)) * rip1;
    
    integral += 0.5 * (fi + fip1) * dr;
  }

  // Multiply by 2π due to polar integration
  integral *= 2.0 * M_PI;
  
  // Normalize such that the integral = 1.0
  Real prefactor = -1.0 / integral;
  
  return -_test[_i][_qp] * Q0 * absorbance * prefactor * exp_term;
}
