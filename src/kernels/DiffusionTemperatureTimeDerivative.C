
#include "DiffusionTemperatureTimeDerivative.h"

registerMooseObject("purpleApp", DiffusionTemperatureTimeDerivative);

InputParameters
DiffusionTemperatureTimeDerivative::validParams()
{
  InputParameters params = ADTimeDerivative::validParams();
  params.addClassDescription(
      "AD Time derivative term $\\rho c_p \\frac{\\partial T}{\\partial t}$ of "
      "the heat equation for quasi-constant specific heat $c_p$ and the density $\\rho$.");
  params.set<bool>("use_displaced_mesh") = true;
	  
  params.addParam<MaterialPropertyName>("rho_c", "The density multiplied by the heat capacity");
  return params;
}

DiffusionTemperatureTimeDerivative::DiffusionTemperatureTimeDerivative(const InputParameters & parameters)
  : ADTimeDerivative(parameters),
    _rho_c(getADMaterialProperty<Real>("rho_c"))
{
}

ADReal
DiffusionTemperatureTimeDerivative::precomputeQpResidual()
{
  return _rho_c[_qp] * ADTimeDerivative::precomputeQpResidual();
}
