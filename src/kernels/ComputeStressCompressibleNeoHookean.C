#include "ComputeStressCompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressCompressibleNeoHookean);

InputParameters
ComputeStressCompressibleNeoHookean::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  params.addRequiredParam<Real>("lambda", "the 1st Lame parameter");

  return params;
}

ComputeStressCompressibleNeoHookean::ComputeStressCompressibleNeoHookean(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),
  
  
	_user_mu(getParam<Real>("mu")),
	_user_lambda(getParam<Real>("lambda"))

{
}



void
ComputeStressCompressibleNeoHookean::computeQpPK2Stress()
{ 
   	// Deformation gradient
	RankTwoTensor F = _F[_qp];
	
	RankTwoTensor C = F.transpose() * F;
	
	RankTwoTensor C_inv = C.inverse();


	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	_S[_qp] = computePiolaKStress2(_user_mu, _user_lambda, C_inv, F);
	
	_C[_qp] = compute_dSdE(_user_mu, _user_lambda, C_inv, F);
}


RankTwoTensor ComputeStressCompressibleNeoHookean::computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F)
{	
	// Jacobian
	Real J = F.det();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	RankTwoTensor S = (mu * (I - C_inv))  +   (lambda * (std::log(J)) * C_inv);
	
	return S;
}
 


RankFourTensor ComputeStressCompressibleNeoHookean::compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F)
{	
	// Jacobian
	Real J = F.det();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	RankFourTensor dSdE;
	
    for (int i = 0; i < 3; ++i) 
	{
        for (int j = 0; j < 3; ++j) 
		{
			for (int k = 0; k < 3; ++k) 
			{
				for (int l = 0; l < 3; ++l) 
				{
					dSdE(i, j, k, l) = (((mu - (lambda * std::log(J))) * C_inv(i,k) * C_inv(l,j)) + ((lambda/2.0) * C_inv(i, j) * C_inv(k,l))) * 2.0;
				}
			}
        }
    }
	
	return dSdE;
}