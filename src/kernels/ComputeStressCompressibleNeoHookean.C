#include "ComputeStressCompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressCompressibleNeoHookean);

InputParameters
ComputeStressCompressibleNeoHookean::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("Calculate Compressible PK2 Stress for Neo-Hookean Model");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  params.addRequiredParam<Real>("lambda", "the 1st Lame parameter");
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ComputeStressCompressibleNeoHookean::ComputeStressCompressibleNeoHookean(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

    /// Get from user, name in input file is in quotes
	_user_mu(getParam<Real>("mu")),
	_user_lambda(getParam<Real>("lambda"))


{
}


void
ComputeStressCompressibleNeoHookean::computeQpPK2Stress()
{
	
	// Deformation gradient
	RankTwoTensor F = _F[_qp];
	
	// Right Cauchy-Green deformation tensor
	RankTwoTensor C = F.transpose() * F;



	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	_S[_qp] = computePiolaKStress2(_user_mu, _user_lambda, C);
	
	_C[_qp] = compute_dSdE(_user_mu, _user_lambda, C);
	
}





RankTwoTensor ComputeStressCompressibleNeoHookean::computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C)
{	
	// Jacobian
	Real J = std::pow(C.det(), 1.0 / 2.0);
	
	RankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	RankTwoTensor I;
	I.setToIdentity();
	
	RankTwoTensor S = (mu * (I - C_inv))  +   (lambda * (std::log(J)) * C_inv);
	
	return S;
}
 


RankFourTensor ComputeStressCompressibleNeoHookean::compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C)
{	
	// Jacobian
	Real J = std::pow(C.det(), 1.0 / 2.0);
	
	RankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	RankTwoTensor I;
	I.setToIdentity();
	
	RankFourTensor C_inv_C_inv = kroneckerProduct4thOrder(C_inv, C_inv);
	
	RankFourTensor first_term = (mu + (lambda/2.0) + (lambda * (std::log(J)))) * C_inv_C_inv;
	
	
	
	RankFourTensor I_I = kroneckerProduct4thOrder(I, I);
	
	
	
	
	RankFourTensor dSdE = innerProduct4thOrder(first_term, I_I);
	
	return dSdE;
}








RankFourTensor ComputeStressCompressibleNeoHookean::innerProduct4thOrder(const RankFourTensor &A, const RankFourTensor &B)
{
    // Initialize the rank-four tensor for the result
    RankFourTensor C;
    
    // Loop through the indices of the resulting tensor C
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            for (int p = 0; p < 3; ++p) {
                for (int q = 0; q < 3; ++q) {
                    // Initialize the sum to zero for each component of C
                    C(i, j, p, q) = 0.0;

                    // Perform the inner product sum over the shared indices k and l
                    for (int k = 0; k < 3; ++k) {
                        for (int l = 0; l < 3; ++l) {
                            C(i, j, p, q) += A(i, j, k, l) * B(k, l, p, q);
                        }
                    }
                }
            }
        }
    }
    
    // Return the resulting fourth-order tensor C
    return C;
}





RankFourTensor ComputeStressCompressibleNeoHookean::kroneckerProduct4thOrder(const RankTwoTensor &A, const RankTwoTensor &B)
{
    // Initialize the rank-four tensor for the result
    RankFourTensor C;
    
    // Loop through the indices of the tensors A and B
    for (int i = 0; i < 3; ++i) {
        for (int j = 0; j < 3; ++j) {
            for (int k = 0; k < 3; ++k) {
                for (int l = 0; l < 3; ++l) {
                    // Compute the Kronecker product by multiplying the respective components of A and B
                    C(i, j, k, l) = A(i, j) * B(k, l);
                }
            }
        }
    }
    
    // Return the resulting fourth-order tensor
    return C;
}
