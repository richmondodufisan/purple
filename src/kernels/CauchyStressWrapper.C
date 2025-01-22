#include "CauchyStressWrapper.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", CauchyStressWrapper);

InputParameters
CauchyStressWrapper::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Wrapper that converts cauchy stress from the new system to old system for use in Dynamics and old stress divergence objects");

  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

CauchyStressWrapper::CauchyStressWrapper(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

	_cauchy_stress_in(getMaterialPropertyByName<RankTwoTensor>(_base_name + "cauchy_stress")),
	_cauchy_jacobian_in(getMaterialPropertyByName<RankFourTensor>(_base_name + "cauchy_jacobian")),

	/// Declare material properties
	_stress(declareProperty<RankTwoTensor>(_base_name + "stress")),
	_Jacobian_mult(declareProperty<RankFourTensor>(_base_name + "Jacobian_mult"))


{
}

void
CauchyStressWrapper::initQpStatefulProperties()
{
	_stress[_qp] = _cauchy_stress_in[_qp];
	_Jacobian_mult[_qp] = _cauchy_jacobian_in[_qp];
}


void
CauchyStressWrapper::computeQpProperties()
{
	_stress[_qp] = _cauchy_stress_in[_qp];
	_Jacobian_mult[_qp] = _cauchy_jacobian_in[_qp];
}

