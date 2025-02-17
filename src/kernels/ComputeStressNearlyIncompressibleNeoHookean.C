#include "ComputeStressNearlyIncompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressNearlyIncompressibleNeoHookean);

InputParameters
ComputeStressNearlyIncompressibleNeoHookean::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  
  params.addRequiredParam<Real>("kappa", "the bulk modulus/incompressibility enforcer");

  return params;
}

ComputeStressNearlyIncompressibleNeoHookean::ComputeStressNearlyIncompressibleNeoHookean(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),
  
  
	_user_mu(getParam<Real>("mu")),
	_user_kappa(getParam<Real>("kappa"))

{
}



void
ComputeStressNearlyIncompressibleNeoHookean::computeQpPK2Stress()
{ 
   	// Deformation gradient
	RankTwoTensor F = _F[_qp];
	
	RankTwoTensor C = F.transpose() * F;


	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	_S[_qp] = computePiolaKStress2(_user_mu, _user_kappa, C, F);
	
	_C[_qp] = compute_dSdE(_user_mu, _user_kappa, C, F);
}


RankTwoTensor ComputeStressNearlyIncompressibleNeoHookean::computePiolaKStress2(const Real &mu, const Real &kappa, const RankTwoTensor &C, const RankTwoTensor &F)
{	
	// Jacobian
	Real J = F.det();
	
	RankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	Real I_1 = C.trace();
	
	Real J_min_23 = std::pow(J, (-2.0/3.0));
	
	RankTwoTensor S = (mu * J_min_23 * (I  -   ((1.0/3.0) * I_1) * C_inv)) -  (kappa * (J - 1) * J * C_inv);
	
	return S;
}
 


RankFourTensor ComputeStressNearlyIncompressibleNeoHookean::compute_dSdE(const Real &mu, const Real &kappa, const RankTwoTensor &C, const RankTwoTensor &F)
{	
	// Jacobian
	Real J = F.det();
	
	RankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	Real I_1 = C.trace();
	
	Real J_min_23 = std::pow(J, (-2.0/3.0));
	
	RankFourTensor dSdE;
	
	
    for (int i = 0; i < 3; ++i) 
	{
        for (int j = 0; j < 3; ++j) 
		{
			for (int k = 0; k < 3; ++k) 
			{
				for (int l = 0; l < 3; ++l) 
				{
					
					Real term1 = (mu/9.0) * I_1 * J_min_23 * C_inv(k, l) * C_inv(i, j);
					
					Real term2 = -(mu/3.0) * J_min_23 * C_inv(i, j) * I(k, l);
					
					Real term3 = (mu/3.0) * J_min_23 * I_1 * C_inv(i, k) * C_inv(l, j);
					
					Real term4 = -(mu/3.0) * J_min_23 * C_inv(k, l) * I(i, j);
					
					
					
					
					Real term5 = -kappa * (J - 1) * J * C_inv(i, k) * C_inv(l, j);
					
					Real term6 = kappa * J * (J/2.0) * C_inv(i, j) * C_inv(k, l);
					
					Real term7 = kappa * (J - 1) * (J/2.0) * C_inv(i, j) * C_inv(k, l);
					
					
					
					
					dSdE(i, j, k, l) = 2 * (term1 + term2 + term3 + term4 + term5 + term6 + term7);
				}
			}
        }
    }
	
	return dSdE;
}