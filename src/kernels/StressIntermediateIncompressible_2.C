#include "StressIntermediateIncompressible_2.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", StressIntermediateIncompressible_2);

InputParameters
StressIntermediateIncompressible_2::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Intermediate file for turning derivative property to material property (rank 4 tensor, tangent operator)");
  
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

StressIntermediateIncompressible_2::StressIntermediateIncompressible_2(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

	/// get material properties
	_dPK1_dW_in(getMaterialPropertyDerivative<RankFourTensor>(_base_name + "dWdF_pF", _base_name + "deformation_gradient")),

	_dPK1_dW_out(declareProperty<RankFourTensor>(_base_name + "dPK1_dW"))

{
}


void
StressIntermediateIncompressible_2::computeQpProperties()
{
	_dPK1_dW_out[_qp] = _dPK1_dW_in[_qp];
}


