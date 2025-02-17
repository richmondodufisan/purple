#include "ComputeStressIncompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressIncompressibleNeoHookean);

InputParameters
ComputeStressIncompressibleNeoHookean::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  params.addRequiredParam<Real>("lambda", "the 1st Lame parameter");
  
  params.addRequiredCoupledVar("pressure", "the pressure variable");

  return params;
}

ComputeStressIncompressibleNeoHookean::ComputeStressIncompressibleNeoHookean(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),
  
  
	_user_mu(getParam<Real>("mu")),
	_user_lambda(getParam<Real>("lambda")),
	
	_pressure(coupledValue("pressure"))

{
}



void
ComputeStressIncompressibleNeoHookean::computeQpPK2Stress()
{ 
   	// Deformation gradient
	RankTwoTensor F = _F[_qp];
	
	RankTwoTensor C = F.transpose() * F;
	
	
	// Pressure
	Real p = _pressure[_qp];


	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	_S[_qp] = computePiolaKStress2(_user_mu, _user_lambda, C, F, p);
	
	_C[_qp] = compute_dSdE(_user_mu, _user_lambda, C, F, p);
}


RankTwoTensor ComputeStressIncompressibleNeoHookean::computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C, const RankTwoTensor &F, const Real &p)
{	
	// Jacobian
	Real J = F.det();
	
	RankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	RankTwoTensor I = RankTwoTensor::Identity();
	
	Real I_1 = C.trace();
	
	Real J_min_23 = std::pow(J, (-2.0/3.0));
	
	RankTwoTensor S = (mu * J_min_23 * (I  -   ((1.0/3.0) * I_1) * C_inv)) -  (p * J * C_inv);
	
	return S;
}
 


RankFourTensor ComputeStressIncompressibleNeoHookean::compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C, const RankTwoTensor &F, const Real &p)
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
					
					Real term5 = p * J * C_inv(i, k) * C_inv(l, j);
					
					Real term6 = -((p * J)/2.0) * C_inv(i, j) * C_inv(k, l);
					
					dSdE(i, j, k, l) = 2 * (term1 + term2 + term3 + term4 + term5 + term6);
				}
			}
        }
    }
	
	return dSdE;
}