#include "FourierHeatEquation.h"
#include "Material.h"
#include "MooseMesh.h"
#include "MooseVariable.h"
#include "SystemBase.h"
#include "NonlinearSystem.h"

#include <cmath>

#include "libmesh/quadrature.h"
#include "libmesh/fe_interface.h"
#include "libmesh/string_to_enum.h"
#include "libmesh/quadrature_gauss.h"
#include "libmesh/quadrature.h"

registerMooseObject("purpleApp", FourierHeatEquation);

InputParameters
FourierHeatEquation::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Solve the Heat Equation with the flux as the variable being acted on");

  params.addRequiredParam<unsigned int>("component_flux",
                                        "An integer corresponding to the direction "
                                        "the variable this kernel acts in. (0 for x, "
                                        "1 for y, 2 for z)");

  params.addParam<std::string>("base_name", "Material property base name");
  
  params.addRequiredCoupledVar("temperature", "the ith component of the flux");
  
  params.addRequiredParam<MaterialPropertyName>("thermal_conductivity", "thermal conductivity of the material");

  return params;
}


FourierHeatEquation::FourierHeatEquation(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    // Get Parameter from user, name in input file is in quotes
    _component_flux(getParam<unsigned int>("component_flux")),
	
	_temp(adCoupledValue("temperature")),
	_kappa(getADMaterialProperty<Real>("thermal_conductivity"))
	
{
}

ADReal
FourierHeatEquation::computeQpResidual()
{
  auto i = _component_flux;

  auto grad_NA = _grad_test[_i][_qp];
  auto NA = _test[_i][_qp];

  auto residual = (_u[_qp] * NA) - (_kappa[_qp] * _temp[_qp] * grad_NA(i));
  
  return residual;
}
