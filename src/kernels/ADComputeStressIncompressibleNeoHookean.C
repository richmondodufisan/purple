#include "ADComputeStressIncompressibleNeoHookean.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ADComputeStressIncompressibleNeoHookean);

InputParameters
ADComputeStressIncompressibleNeoHookean::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required and calculate the strain energy, stress, and tangent for an incompressible Neo-Hookean solid");

  params.addRequiredParam<Real>("mu", "the shear modulus");
  
  params.addRequiredCoupledVar("pressure", "the pressure variable");

  return params;
}

ADComputeStressIncompressibleNeoHookean::ADComputeStressIncompressibleNeoHookean(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),


    // Get from user, name in input file is in quotes
	_user_mu(getParam<Real>("mu")),
	
	_pressure(adCoupledValue("pressure")),
	
	_deformation_gradient(getMaterialPropertyByName<RankTwoTensor>("deformation_gradient")),

	// Declare material properties
	
	_ad_cauchy_stress(declareADProperty<RankTwoTensor>("ad_cauchy_stress"))


{
}


void
ADComputeStressIncompressibleNeoHookean::computeQpProperties()
{
   	// Deformation gradient
	auto F = _deformation_gradient[_qp];
  
    auto J = F.det();
	
	RankTwoTensor C = F.transpose() * F;
	
	
	// Pressure
	ADReal p = _pressure[_qp];


	
	// _S and _C are the names of the stress and tangent in the class it inherits from
	// That is, the PK2 Template Class
	// These are the final submissions of stress and tangent operator
	
	auto S = computePiolaKStress2(_user_mu, C, F, p);
	
	_ad_cauchy_stress[_qp] = (1.0 / J) * (F * (S * F.transpose()));
	
	// std::cout << "pressure = " << p << std::endl;
}



ADRankTwoTensor ADComputeStressIncompressibleNeoHookean::computePiolaKStress2(const ADReal &mu, const ADRankTwoTensor &C, const ADRankTwoTensor &F, const ADReal &p)
{	
	// Jacobian
	auto J = F.det();
	
	ADRankTwoTensor C_inv = C.inverse();
	
	// Identity Tensor
	ADRankTwoTensor I = RankTwoTensor::Identity();
	
	ADReal I_1 = C.trace();
	
	ADReal J_min_23 = std::pow(J, (-2.0/3.0));
	
	ADRankTwoTensor S = (mu * J_min_23 * (I  -   ((1.0/3.0) * I_1) * C_inv)) + (p * C_inv);
	
	return S;
}