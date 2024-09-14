#include "ComputeStrainEnergyNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStrainEnergyNeoHookean);

InputParameters
ComputeStrainEnergyNeoHookean::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu_0", "the initial shear modulus");
  params.addParam<std::string>("base_name", "", "Base name for material properties");

  return params;
}

ComputeStrainEnergyNeoHookean::ComputeStrainEnergyNeoHookean(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    /// Get Parameter from user, name in input file is in quotes
	_user_mu_0(getParam<Real>("mu_0")),
	
	/// Get deformation gradient, declared by strain object	
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),

	/// Declare material properties
	_strain_energy(declareProperty<Real>(_base_name + "strain_energy")),
	_dWdF(declarePropertyDerivative<RankTwoTensor>(_base_name + "strain_energy", _base_name + "deformation_gradient")),	// this is the stress
	_d2WdF2(declarePropertyDerivative<RankFourTensor>(_base_name + "strain_energy", _base_name + "deformation_gradient", _base_name + "deformation_gradient")) //this is the tangent operator


{
}


void
ComputeStrainEnergyNeoHookean::computeQpProperties()
{
	auto mu_0 = _user_mu_0;
	
	auto F = _deformation_gradient[_qp];
	
	// Right Cauchy-Green deformation tensor
	auto C = F.transpose() * F;
	
	// First invariant, equivalent to lambda_1^2 + lambda_2^2 + lambda_3^2
	auto I_1 = C.trace();
	
	
	_strain_energy[_qp] = (mu_0/2.0) * (I_1 - 3);
	
}


