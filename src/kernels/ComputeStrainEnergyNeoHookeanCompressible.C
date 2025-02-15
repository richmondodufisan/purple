#include "ComputeStrainEnergyNeoHookeanCompressible.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStrainEnergyNeoHookeanCompressible);

InputParameters
ComputeStrainEnergyNeoHookeanCompressible::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  params.addRequiredParam<Real>("lambda", "the 1st Lame parameter");
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ComputeStrainEnergyNeoHookeanCompressible::ComputeStrainEnergyNeoHookeanCompressible(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

    /// Get from user, name in input file is in quotes
	_user_mu(getParam<Real>("mu")),
	_user_lambda(getParam<Real>("lambda")),
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),

	/// Declare material properties
	_strain_energy(declareProperty<Real>(_base_name + "strain_energy")),
	_PK2(declareProperty<RankTwoTensor>(_base_name + "PK2")),
	_dPK2_dE(declareProperty<RankFourTensor>(_base_name + "dPK2_dE"))


{
}


void
ComputeStrainEnergyNeoHookeanCompressible::computeQpProperties()
{
	// // Deformation gradient
	RankTwoTensor F = _deformation_gradient[_qp];
	// setNearZeroToZero(F, 1e-15);
	
	// // Right Cauchy-Green deformation tensor
	RankTwoTensor C = F.transpose() * F;
	// setNearZeroToZero(C, 1e-15);
	
	RankTwoTensor I;
	I.setToIdentity();
	
	// // Green Lagrange Strain Tensor
	RankTwoTensor E = 0.5 * (C - I);
	// setNearZeroToZero(E, 1e-15);
	
	
	_strain_energy[_qp] = computeStrainEnergy(_user_mu, _user_lambda, C);
	
	_PK2[_qp] = computePiolaKStress2(_user_mu, _user_lambda, C);
	
	_dPK2_dE[_qp] = compute_dPK2dE(_user_mu, _user_lambda, C);
}












Real ComputeStrainEnergyNeoHookeanCompressible::computeStrainEnergy(const Real &mu, const Real &lambda, const RankTwoTensor &C)
{
	Real J = std::pow(C.det(), 1.0 / 2.0);
	
	// First invariant
	double I_1 = C.trace();
	
	
	RankTwoTensor C_squared = C * C;
	
	// Second invariant
	double I_2 = 0.5 * (  (std::pow(I_1, 1.0 / 2.0))  -   C_squared.trace()   );
	

	double strain_energy = (0.5 * mu * (I_1 - 3)) - (mu * std::log(J))  +  (0.5 * lambda * std::pow((std::log(J)), 1.0 / 2.0));
	
	return strain_energy;
}









RankTwoTensor ComputeStrainEnergyNeoHookeanCompressible::compute_dWdC(const Real &mu, const Real &lambda, const RankTwoTensor &C) 
{
    // Initialize derivative
	RankTwoTensor dWdC;
    
    // Compute the scalar function for the original tensor
    Real W = computeStrainEnergy(mu, lambda, C);

    // Loop over all components of the tensor to compute the derivative
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            // Compute an optimal epsilon for this component
            Real epsilon = chooseOptimalEpsilon(C(i, j));
            
            // Create a copy of the tensor to perturb
            RankTwoTensor C_perturbed = C;
            C_perturbed(i, j) += epsilon;

            // Evaluate the scalar function at the perturbed tensor
            Real W_perturbed = computeStrainEnergy(mu, lambda, C_perturbed);

            // Compute the finite difference derivative and store it in the dfdT tensor
			// Recall epsilon = C(i,j) - C_perturbed(i,j)
			
            dWdC(i, j) = (W_perturbed - W) / epsilon;
        }
    }

    // Return the tensor of derivatives
    return dWdC;
}










// Calculate the Stress
RankTwoTensor ComputeStrainEnergyNeoHookeanCompressible::computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C)
{	
	RankTwoTensor dWdC = compute_dWdC(mu, lambda, C);
	
	RankTwoTensor thepk2_stress = 2.0 * dWdC;
	
	return thepk2_stress;
}











RankFourTensor ComputeStrainEnergyNeoHookeanCompressible::compute_dPK2dE(const Real &mu, const Real &lambda, const RankTwoTensor &C)
{
    RankTwoTensor I;
	I.setToIdentity();
	
	// Green Lagrange Strain Tensor
	RankTwoTensor E = 0.5 * (C - I);
	
    // Initialize derivative
    RankFourTensor dPK2dE;
	
	// Compute the original PK2
    RankTwoTensor PK2_original = computePiolaKStress2(mu, lambda, C);

    // Loop over all components of tensor A
    for (int i = 0; i < 3; i++) 
	{
        for (int j = 0; j < 3; j++) 
		{           

            // Loop over all components of tensor B (perturb tensor)
            for (int k = 0; k < 3; k++) 
			{
                for (int l = 0; l < 3; l++) 
				{
					// Compute an optimal epsilon for this component
                    Real epsilon = chooseOptimalEpsilon(E(k, l));
					
                    // Create a copy of B to perturb
					RankTwoTensor E_perturbed = E;

					// Perturb the (k, l) component by epsilon
					E_perturbed(k, l) += epsilon;

					// Evaluate the PK2 at the perturbed tensor
					RankTwoTensor PK2_perturbed = computePiolaKStress2(mu, lambda, C);

                    // Compute the finite difference derivative and store it in dAdB
                    dPK2dE(i, j, k, l) = (PK2_perturbed(i, j) - PK2_original(i, j)) / epsilon;
                }
            }
        }
    }

    // Return the rank-four tensor of derivatives
    return dPK2dE;
}










// Function to dynamically choose epsilon
Real ComputeStrainEnergyNeoHookeanCompressible::chooseOptimalEpsilon(const Real &value) 
{
    Real epsilon_machine = std::numeric_limits<Real>::epsilon();
	
    return std::max(epsilon_machine, std::sqrt(epsilon_machine) * std::abs(value));
}








// void ComputeStrainEnergyNeoHookeanCompressible::setNearZeroToZero(RankTwoTensor &tensor, const Real tolerance)
// {
    // for (unsigned int i = 0; i < 3; ++i)
    // {
        // for (unsigned int j = 0; j < 3; ++j)
        // {
            // if (std::fabs(tensor(i, j)) < tolerance)
            // {
                // tensor(i, j) = 0.0;
            // }
        // }
    // }
// }