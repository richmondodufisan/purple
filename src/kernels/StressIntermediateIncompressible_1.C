#include "StressIntermediateIncompressible_1.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", StressIntermediateIncompressible_1);

InputParameters
StressIntermediateIncompressible_1::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Intermediate file for calculating incompressible stress based on derivative of strain energy");
  
  params.addParam<std::string>("base_name", "", "Base name for material properties");
  
  params.addRequiredCoupledVar("pressure", "the pressure, a lagrange multiplier to enforce incompressibility");

  return params;
}

StressIntermediateIncompressible_1::StressIntermediateIncompressible_1(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

	/// Get deformation gradient, declared by strain object	
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),

	/// get material properties
	_dWdF(getMaterialPropertyDerivative<RankTwoTensor>(_base_name + "strain_energy", _base_name + "deformation_gradient")),
	
	
	_pressure(coupledValue("pressure")),

	_dWdF_pF_out(declareProperty<RankTwoTensor>(_base_name + "dWdF_pF")),
	_tangent_out(declarePropertyDerivative<RankFourTensor>(_base_name + "dWdF_pF", _base_name + "deformation_gradient"))

{
}


void
StressIntermediateIncompressible_1::computeQpProperties()
{
	auto F = _deformation_gradient[_qp];
	
	_dWdF_pF_out[_qp] = _dWdF[_qp] + (_pressure[_qp] * F.inverse());
}


