#include "ADComputeStressCompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ADComputeStressCompressibleNeoHookean);

InputParameters
ADComputeStressCompressibleNeoHookean::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required for concrete fracture");

  params.addParam<std::string>("base_name", "Material property base name");

  params.addRequiredParam<Real>("mu", "shear modulus");
  params.addRequiredParam<Real>("lambda", "Lame parameter");
  

  return params;
}

ADComputeStressCompressibleNeoHookean::ADComputeStressCompressibleNeoHookean(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),


	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    // Get Parameter from user, name in input file is in quotes
	_user_mu(getParam<Real>(_base_name + "mu")),
    _user_lambda(getParam<Real>(_base_name + "lambda")),
	
	_deformation_gradient(getADMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),
	
	_stress(declareADProperty<RankTwoTensor>(_base_name + "stress"))


{
}


void
ADComputeStressCompressibleNeoHookean::computeQpProperties()
{
   	// Deformation gradient
	ADRankTwoTensor F = _deformation_gradient[_qp];
	
	ADRankTwoTensor C = F.transpose() * F;
	
	ADRankTwoTensor C_inv = C.inverse();


	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	_stress[_qp] = computePiolaKStress2(_user_mu, _user_lambda, C_inv, F);
	
}


ADRankTwoTensor ADComputeStressCompressibleNeoHookean::computePiolaKStress2(const ADReal &mu, const ADReal &lambda, const ADRankTwoTensor &C_inv, const ADRankTwoTensor &F)
{	
	// Jacobian
	ADReal J = F.det();
	
	// Identity Tensor
	ADRankTwoTensor I = RankTwoTensor::Identity();
	
	ADRankTwoTensor S = (mu * (I - C_inv))  +   (lambda * (std::log(J)) * C_inv);
	
	return S;
}
 


ADRankFourTensor ADComputeStressCompressibleNeoHookean::compute_dSdE(const ADReal &mu, const ADReal &lambda, const ADRankTwoTensor &C_inv, const ADRankTwoTensor &F)
{	
	// Jacobian
	ADReal J = F.det();
	
	// Identity Tensor
	ADRankTwoTensor I = RankTwoTensor::Identity();
	
	ADRankFourTensor dSdE;
	
    for (int i = 0; i < 3; ++i) 
	{
        for (int j = 0; j < 3; ++j) 
		{
			for (int p = 0; p < 3; ++p) 
			{
				for (int q = 0; q < 3; ++q) 
				{
					dSdE(i, j, p, q) = (((mu - (lambda * std::log(J))) * C_inv(i,p) * C_inv(q,j)) + ((lambda/2.0) * C_inv(i, j) * C_inv(p,q))) * 2.0;
				}
			}
        }
    }
	
	return dSdE;
}