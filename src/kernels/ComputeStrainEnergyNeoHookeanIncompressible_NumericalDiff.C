#include "ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff);

InputParameters
ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu_0", "the initial shear modulus");
  params.addRequiredCoupledVar("pressure_var", "the pressure lagrangian multiplier");
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") && !getParam<std::string>("base_name").empty() 
                ? getParam<std::string>("base_name") + "_" 
                : ""),

    /// Get from user, name in input file is in quotes
	_user_mu_0(getParam<Real>("mu_0")),
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),
	_pressure(coupledValue("pressure_var")),

	/// Declare material properties
	_strain_energy(declareProperty<Real>(_base_name + "strain_energy")),
	_PK1(declareProperty<RankTwoTensor>(_base_name + "PK1")),
	_dPK1_dF(declareProperty<RankFourTensor>(_base_name + "dPK1_dF"))


{
}


void
ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::computeQpProperties()
{
	// Deformation gradient
	RankTwoTensor F = _deformation_gradient[_qp];
	setNearZeroToZero(F, 1e-9);
	
	// pressure
	Real p = _pressure[_qp];
	if (std::fabs(p) < 1e-9)
	{
		p = 0;
	}
	
	_strain_energy[_qp] = computeStrainEnergy(_user_mu_0, F);
	
	_PK1[_qp] = computePiolaKStress1(_user_mu_0, F, p);
	
	_dPK1_dF[_qp] = compute_dPK1dF(_user_mu_0, F, p); 
}












Real ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::computeStrainEnergy(const Real &mu_0,const RankTwoTensor &F)
{
	double J = F.det();
	
	// Isochoric deformation_gradient
	RankTwoTensor F_iso = std::pow(J, -1.0 / 3.0) * F;
	
	// Right Cauchy-Green deformation tensor
	RankTwoTensor C_iso = F_iso.transpose() * F_iso;
	
	// First invariant, equivalent to lambda_1^2 + lambda_2^2 + lambda_3^2
	double I_1 = C_iso.trace();
	
	double strain_energy = (mu_0/2.0) * (I_1 - 3);
	
	return strain_energy;
}









// Compute the numerical derivative of a scalar function w.r.t a tensor_ij

RankTwoTensor ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::compute_dWdF(const Real &mu_0, const RankTwoTensor &F) 
{
	// Initialize tolerance
	Real epsilon = 1e-6;
	
	// Initialize derivative
	RankTwoTensor dWdF;
	
    // Compute the scalar function for the original tensor
    Real W = computeStrainEnergy(mu_0, F);

    // Loop over all components of the tensor to compute the derivative
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            // Create a copy of the tensor to perturb
            RankTwoTensor F_perturbed = F;

            // Perturb the (i, j) component by epsilon
            F_perturbed(i, j) += epsilon;

            // Evaluate the scalar function at the perturbed tensor
            Real W_perturbed = computeStrainEnergy(mu_0, F_perturbed);

            // Compute the finite difference derivative and store it in the dfdT tensor
            dWdF(i, j) = (W_perturbed - W) / epsilon;
        }
    }

    // Return the tensor of derivatives
    return dWdF;
}













// Calculate the Stress
// Calculate the Stress
RankTwoTensor ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::computePiolaKStress1(const Real &mu_0, const RankTwoTensor &F, const Real &p)
{
	RankTwoTensor F_inv = F.inverse();
	
	Real J = F.det();
	
	RankTwoTensor dWdF = compute_dWdF(mu_0, F);
	
	RankTwoTensor thepk1_stress = dWdF - (p * J * F_inv.transpose());
	
	return thepk1_stress;
}














RankFourTensor ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::compute_dPK1dF(const Real &mu_0, const RankTwoTensor &F, const Real &p) 
{
	// Initialize tolerance
	 Real epsilon = 1e-6;
	
    // Initialize derivative
    RankFourTensor dPK1dF;
	
	// Compute the original PK1
    RankTwoTensor PK1_original = computePiolaKStress1(mu_0, F, p);

    // Loop over all components of tensor A
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {           


            // Loop over all components of tensor B (perturb tensor)
            for (int k = 0; k < 3; k++) {
                for (int l = 0; l < 3; l++) {
					
                    // Create a copy of B to perturb
					RankTwoTensor F_perturbed = F;

					// Perturb the (k, l) component by epsilon
					F_perturbed(k, l) += epsilon;

					// Evaluate the PK1 at the perturbed tensor
					RankTwoTensor PK1_perturbed = computePiolaKStress1(mu_0, F_perturbed, p);

                    // Compute the finite difference derivative and store it in dAdB
                    dPK1dF(i, j, k, l) = (PK1_perturbed(i, j) - PK1_original(i, j)) / epsilon;
                }
            }
        }
    }

    // Return the rank-four tensor of derivatives
    return dPK1dF;
}










void ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff::setNearZeroToZero(RankTwoTensor &tensor, const Real tolerance)
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