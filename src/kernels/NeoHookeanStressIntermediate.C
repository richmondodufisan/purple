#include "NeoHookeanStressIntermediate.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", NeoHookeanStressIntermediate);

InputParameters
NeoHookeanStressIntermediate::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Intermediate file for calculating Neo Hookean Stress since the Base PK1 class doesn't do derivatives");
  
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

NeoHookeanStressIntermediate::NeoHookeanStressIntermediate(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

	/// get material properties
	_dWdF(getMaterialPropertyDerivative<RankTwoTensor>(_base_name + "strain_energy", _base_name + "deformation_gradient")),	// this is the stress
	_d2WdF2(getMaterialPropertyDerivative<RankFourTensor>(_base_name + "strain_energy", _base_name + "deformation_gradient", _base_name + "deformation_gradient")), //this is the tangent operator

	_dWdF_out(declareProperty<RankTwoTensor>(_base_name + "dWdF")),
	_d2WdF2_out(declareProperty<RankFourTensor>(_base_name + "d2WdF2"))

{
}


void
NeoHookeanStressIntermediate::computeQpProperties()
{
	_dWdF_out[_qp] = _dWdF[_qp];
	_d2WdF2_out[_qp] = _d2WdF2[_qp];
}


