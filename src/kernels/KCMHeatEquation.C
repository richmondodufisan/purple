#include "KCMHeatEquation.h"
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

registerMooseObject("purpleApp", KCMHeatEquation);

InputParameters
KCMHeatEquation::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Solve the Heat Equation with the flux as the variable being acted on");

  params.addRequiredParam<unsigned int>("component_flux",
                                        "An integer corresponding to the direction "
                                        "the variable this kernel acts in. (0 for x, "
                                        "1 for y, 2 for z)");
										
  params.addRequiredCoupledVar("temperature", "the temperature corresponding to the flux");
  
  params.addRequiredParam<MaterialPropertyName>("thermal_conductivity", "thermal conductivity of the material");
  params.addRequiredParam<MaterialPropertyName>("length_scale", "nonlocal length scale");
  params.addRequiredParam<MaterialPropertyName>("alpha", "alpha parameter");

  params.addParam<std::string>("base_name", "Material property base name");
  
  params.addRequiredCoupledVar("q_x", "flux in x-direction");
  params.addRequiredCoupledVar("q_y", "flux in y-direction");
  params.addRequiredCoupledVar("q_z", "flux in z-direction");

  return params;
}


KCMHeatEquation::KCMHeatEquation(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    // Get Parameter from user, name in input file is in quotes
    _component_flux(getParam<unsigned int>("component_flux")),
	
	_grad_temp(adCoupledGradient("temperature")),
	
	_q_x(adCoupledValue("q_x")),
	_q_y(adCoupledValue("q_y")),
	_q_z(adCoupledValue("q_z")),
	
	_grad_q_x(adCoupledGradient("q_x")),
	_grad_q_y(adCoupledGradient("q_y")),
	_grad_q_z(adCoupledGradient("q_z")),
	
	_kappa(getADMaterialProperty<Real>("thermal_conductivity")),
	_length_scale(getADMaterialProperty<Real>("length_scale")),
	_alpha(getADMaterialProperty<Real>("alpha"))
	
{
}

ADReal
KCMHeatEquation::computeQpResidual()
{
  auto i = _component_flux;

  auto grad_NA = _grad_test[_i][_qp];
  auto NA = _test[_i][_qp];
  
  auto term1 = _u[_qp] * NA;
  auto term2 = _kappa[_qp] * _grad_temp[_qp](i) * NA;
  auto term3 = _length_scale[_qp] * _length_scale[_qp] * ( (_grad_u[_qp](0)*grad_NA(0)) + (_grad_u[_qp](1)*grad_NA(1)) + (_grad_u[_qp](2)*grad_NA(2)) );
  auto term4 = _length_scale[_qp] * _length_scale[_qp] * _alpha[_qp] * ( _grad_q_x[_qp](0) + _grad_q_y[_qp](1) + _grad_q_z[_qp](2)) * grad_NA(i);

  auto residual = term1 + term2 + term3 + term4;
  
  return  residual;
}
