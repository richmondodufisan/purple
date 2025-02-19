#include "ADCauchyStressWrapper.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ADCauchyStressWrapper);

InputParameters
ADCauchyStressWrapper::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Wrapper that converts cauchy stress from the new system to old system for use in Dynamics and old stress divergence objects - AD version");

  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ADCauchyStressWrapper::ADCauchyStressWrapper(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

	_cauchy_stress_in(getADMaterialPropertyByName<RankTwoTensor>(_base_name + "ad_cauchy_stress")),

	/// Declare material properties
	_stress(declareADProperty<RankTwoTensor>(_base_name + "stress"))


{
}

void
ADCauchyStressWrapper::initQpStatefulProperties()
{
	_stress[_qp] = _cauchy_stress_in[_qp];
}


void
ADCauchyStressWrapper::computeQpProperties()
{
	_stress[_qp] = _cauchy_stress_in[_qp];
}

