#include "HeatConductionSteadyImag.h"
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

registerMooseObject("purpleApp", HeatConductionSteadyImag);

InputParameters
HeatConductionSteadyImag::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Solve the Heat Equation in the Fourier Space to get the steady state response");
										
  params.addRequiredCoupledVar("real_temp", "the imaginiary part of the temperature variable");
  
  params.addRequiredParam<MaterialPropertyName>("thermal_conductivity", "thermal conductivity of the material");
  params.addRequiredParam<MaterialPropertyName>("heat_capacity", "heat capacity of the material");
  params.addRequiredParam<MaterialPropertyName>("omega", "angular frequency being considered");
  params.addRequiredParam<MaterialPropertyName>("density", "density of the material");

  params.addParam<std::string>("base_name", "Material property base name");

  return params;
}


HeatConductionSteadyImag::HeatConductionSteadyImag(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    // Get Parameter from user, name in input file is in quotes
	
	_X(adCoupledValue("real_temp")),
	
	_kappa(getADMaterialProperty<Real>("thermal_conductivity")),
	_c(getADMaterialProperty<Real>("heat_capacity")),
	_omega(getADMaterialProperty<Real>("omega")),
	_rho(getADMaterialProperty<Real>("density"))
	
{
}

ADReal
HeatConductionSteadyImag::computeQpResidual()
{
  auto grad_NA = _grad_test[_i][_qp];
  auto NA = _test[_i][_qp];
  
  auto residual = (_kappa[_qp] * _grad_u[_qp] * grad_NA) + (_omega[_qp] * _rho[_qp] * _c[_qp] * _X[_qp] * NA);
  
  return  residual;
}
