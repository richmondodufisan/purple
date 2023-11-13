
#include "KCMHeatEquationTimeDerivative.h"

registerMooseObject("purpleApp", KCMHeatEquationTimeDerivative);

InputParameters
KCMHeatEquationTimeDerivative::validParams()
{
  InputParameters params = ADTimeDerivative::validParams();
  params.addClassDescription(
      "AD Time derivative term $\\rho c_p \\frac{\\partial T}{\\partial t}$ of "
      "the heat equation for quasi-constant specific heat $c_p$ and the density $\\rho$.");
  params.set<bool>("use_displaced_mesh") = true;
	  
  params.addParam<MaterialPropertyName>("relaxation_time", "The density multiplied by the heat capacity");
  return params;
}

KCMHeatEquationTimeDerivative::KCMHeatEquationTimeDerivative(const InputParameters & parameters)
  : ADTimeDerivative(parameters),
    _tau(getADMaterialProperty<Real>("relaxation_time"))
{
}

ADReal
KCMHeatEquationTimeDerivative::precomputeQpResidual()
{
  return _tau[_qp] * ADTimeDerivative::precomputeQpResidual();
}
