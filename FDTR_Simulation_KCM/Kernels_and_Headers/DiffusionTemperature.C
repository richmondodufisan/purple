#include "DiffusionTemperature.h"
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

registerMooseObject("purpleApp", DiffusionTemperature);

InputParameters
DiffusionTemperature::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Solve the Heat Equation with the temperature as the variable being acted on, and independent flux fields");

  params.addParam<std::string>("base_name", "Material property base name");
  
  params.addRequiredCoupledVar("q_x", "flux in x-direction");
  params.addRequiredCoupledVar("q_y", "flux in y-direction");
  params.addRequiredCoupledVar("q_z", "flux in z-direction");

  return params;
}


DiffusionTemperature::DiffusionTemperature(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    // Get Parameter from user, name in input file is in quotes
	_q_x(adCoupledValue("q_x")),
	_q_y(adCoupledValue("q_y")),
	_q_z(adCoupledValue("q_z"))
	
{
}

ADReal
DiffusionTemperature::computeQpResidual()
{
  auto grad_NA = _grad_test[_i][_qp];
  auto NA = _test[_i][_qp];

  auto residual = -( ( _q_x[_qp] *  grad_NA(0)) + ( _q_y[_qp] *  grad_NA(1)) + ( _q_z[_qp] *  grad_NA(2)) );
  
  return  residual;
}
