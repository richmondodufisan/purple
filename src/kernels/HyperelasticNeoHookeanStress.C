#include "HyperelasticNeoHookeanStress.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", HyperelasticNeoHookeanStress);

InputParameters
HyperelasticNeoHookeanStress::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  params.addRequiredParam<Real>("lambda", "the 1st Lame parameter");

  return params;
}

HyperelasticNeoHookeanStress::HyperelasticNeoHookeanStress(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),
  
  
	_user_mu(getParam<Real>("mu")),
	_user_lambda(getParam<Real>("lambda"))

{
}



void
HyperelasticNeoHookeanStress::computeQpPK2Stress()
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


RankTwoTensor HyperelasticNeoHookeanStress::computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F)
{	
	// Jacobian
	Real J = F.det();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	RankTwoTensor S = (mu * (I - C_inv))  +   (lambda * (std::log(J)) * C_inv);
	
	return S;
}
 


RankFourTensor HyperelasticNeoHookeanStress::compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F)
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