#include "ComputeStrainEnergyNeoHookeanNearlyIncompressible.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStrainEnergyNeoHookeanNearlyIncompressible);

InputParameters
ComputeStrainEnergyNeoHookeanNearlyIncompressible::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu_0", "the initial shear modulus");
  params.addRequiredParam<Real>("poissons_ratio", "the poissons ratio of the nearly incompressible material");
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ComputeStrainEnergyNeoHookeanNearlyIncompressible::ComputeStrainEnergyNeoHookeanNearlyIncompressible(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

    /// Get from user, name in input file is in quotes
	_user_mu_0(getParam<Real>("mu_0")),
	_user_nu(getParam<Real>("poissons_ratio")),
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),

	/// Declare material properties
	_strain_energy(declareProperty<Real>(_base_name + "strain_energy")),
	_PK2(declareProperty<RankTwoTensor>(_base_name + "PK2")),
	_dPK2_dE(declareProperty<RankFourTensor>(_base_name + "dPK2_dE"))


{
}


void
ComputeStrainEnergyNeoHookeanNearlyIncompressible::computeQpProperties()
{
	// Deformation gradient
	RankTwoTensor F = _deformation_gradient[_qp];
	setNearZeroToZero(F, 1e-12);
	
	// Right Cauchy-Green deformation tensor
	RankTwoTensor C = F.transpose() * F;
	setNearZeroToZero(C, 1e-12);
	
	RankTwoTensor I;
	I.setToIdentity();
	
	// Green Lagrange Strain Tensor
	RankTwoTensor E = 0.5 * (C - I);
	setNearZeroToZero(E, 1e-12);
	
	
	_strain_energy[_qp] = computeStrainEnergy(_user_mu_0, C);
	
	_PK2[_qp] = computePiolaKStress2(_user_mu_0, E, _user_nu);
	
	_dPK2_dE[_qp] = compute_dPK2dE(_user_mu_0, E, _user_nu);
}












Real ComputeStrainEnergyNeoHookeanNearlyIncompressible::computeStrainEnergy(const Real &mu_0, const RankTwoTensor &C)
{
	Real J = std::pow(C.det(), 1.0 / 2.0);
	
	// Isochoric Right Cauchy-Green deformation tensor
	RankTwoTensor C_iso = std::pow(J, -2.0 / 3.0) * C;
	
	// First invariant, equivalent to lambda_1^2 + lambda_2^2 + lambda_3^2
	double I_1 = C_iso.trace();
	
	double strain_energy = (mu_0/2.0) * (I_1 - 3);
	
	return strain_energy;
}









// Compute the numerical derivative of a scalar function w.r.t a tensor_ij

RankTwoTensor ComputeStrainEnergyNeoHookeanNearlyIncompressible::compute_dWdC(const Real &mu_0, const RankTwoTensor &C) 
{
	// Initialize perturbation
	Real epsilon = 1e-6;
	
	// Initialize derivative
	RankTwoTensor dWdC;
	
    // Compute the scalar function for the original tensor
    Real W = computeStrainEnergy(mu_0, C);

    // Loop over all components of the tensor to compute the derivative
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            // Create a copy of the tensor to perturb
            RankTwoTensor C_perturbed = C;

            // Perturb the (i, j) component by epsilon
            C_perturbed(i, j) += epsilon;

            // Evaluate the scalar function at the perturbed tensor
            Real W_perturbed = computeStrainEnergy(mu_0, C_perturbed);

            // Compute the finite difference derivative and store it in the dfdT tensor
            dWdC(i, j) = (W_perturbed - W) / epsilon;
        }
    }

    // Return the tensor of derivatives
    return dWdC;
}













// Calculate the Stress
RankTwoTensor ComputeStrainEnergyNeoHookeanNearlyIncompressible::computePiolaKStress2(const Real &mu_0, const RankTwoTensor &E, const Real &nu)
{
	RankTwoTensor I;
	I.setToIdentity();
	
	RankTwoTensor C = (2 * E) + I;
	
	Real J = std::pow(C.det(), 1.0 / 2.0);
	
	RankTwoTensor dWdC = compute_dWdC(mu_0, C);
	
	// Calculate bulk modulus
	Real K = ((2 * mu_0) * (1 + nu)) / (3 * (1 - 2*nu));
	
	// pressure = Quadratic dW_vol/dJ
	// Real p = -K * (J - 1);
	
	// pressure = Harman-Neff dW_vol/dJ
	Real p = (-0.1 * K) * (std::pow(J, 4.0) - std::pow(J, -6.0));
	
	RankTwoTensor thepk2_stress = (-p * J * C.inverse()) + (2 * dWdC);
	// RankTwoTensor thepk2_stress = (2 * dWdC);
	
	return thepk2_stress;
}














RankFourTensor ComputeStrainEnergyNeoHookeanNearlyIncompressible::compute_dPK2dE(const Real &mu_0, const RankTwoTensor &E, const Real &nu)
{
	// Initialize perturbation
	 Real epsilon = 1e-6;
	
    // Initialize derivative
    RankFourTensor dPK2dE;
	
	
	// Compute the original PK2
    RankTwoTensor PK2_original = computePiolaKStress2(mu_0, E, nu);

    // Loop over all components of tensor A
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {           


            // Loop over all components of tensor B (perturb tensor)
            for (int k = 0; k < 3; k++) {
                for (int l = 0; l < 3; l++) {
					
                    // Create a copy of B to perturb
					RankTwoTensor E_perturbed = E;

					// Perturb the (k, l) component by epsilon
					E_perturbed(k, l) += epsilon;

					// Evaluate the PK2 at the perturbed tensor
					RankTwoTensor PK2_perturbed = computePiolaKStress2(mu_0, E_perturbed, nu);

                    // Compute the finite difference derivative and store it in dAdB
                    dPK2dE(i, j, k, l) = (PK2_perturbed(i, j) - PK2_original(i, j)) / epsilon;
                }
            }
        }
    }

    // Return the rank-four tensor of derivatives
    return dPK2dE;
}









void ComputeStrainEnergyNeoHookeanNearlyIncompressible::setNearZeroToZero(RankTwoTensor &tensor, const Real tolerance)
{
    for (unsigned int i = 0; i < 3; ++i)
    {
        for (unsigned int j = 0; j < 3; ++j)
        {
            if (std::fabs(tensor(i, j)) < tolerance)
            {
                tensor(i, j) = 0.0;
            }
        }
    }
}