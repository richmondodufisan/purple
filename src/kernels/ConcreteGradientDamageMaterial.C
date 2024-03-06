#include "ConcreteGradientDamageMaterial.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ConcreteGradientDamageMaterial);

InputParameters
ConcreteGradientDamageMaterial::validParams()
{
  InputParameters params = ADMaterial::validParams();
  params.addClassDescription("Collect material properties required for concrete fracture");

  params.addRequiredParam<Real>("nu", "poisson's ratio");
  params.addRequiredParam<Real>("kappa_0", "Initial kappa");
  params.addRequiredParam<Real>("alpha", "alpha parameter");
  params.addRequiredParam<Real>("beta", "beta parameter");
  params.addRequiredParam<Real>("k", "concrete tensile/comp ratio");
  params.addRequiredParam<Real>("nonlocal_radius", "length scale");
  
  params.addRequiredCoupledVar("nonlocal_strain", "the non local equivalent strain");
  

  return params;
}

ConcreteGradientDamageMaterial::ConcreteGradientDamageMaterial(const InputParameters & parameters)
  : DerivativeMaterialInterface<Material>(parameters),

    /// Get Parameter from user, name in input file is in quotes
	_user_nu(getParam<Real>("nu")),
    _user_kappa_0(getParam<Real>("kappa_0")),
	_user_alpha(getParam<Real>("alpha")),
	_user_beta(getParam<Real>("beta")),
    _user_k(getParam<Real>("k")),
    _user_nonlocal_radius(getParam<Real>("nonlocal_radius")),
	


	_nonlocal_radius(declareADProperty<Real>("nonlocal_radius")),
	_D(declareADProperty<Real>("damage")),
	_kappa(declareADProperty<Real>("kappa")),
	
	_stress(getADMaterialPropertyByName<RankTwoTensor>("stress")),
	_strain(getADMaterialPropertyByName<RankTwoTensor>("mechanical_strain")),
	
	_kappa_bar(adCoupledValue("nonlocal_strain")),
	
	_seeoutput(declareADProperty<Real>("debug_purposes"))

{
}


void
ConcreteGradientDamageMaterial::computeQpProperties()
{
	n_dim = 3;
	
	// Define Material Properties
	auto nu = _user_nu;
	auto kappa_0 = _user_kappa_0;
	auto alpha = _user_alpha;
	auto beta = _user_beta;
	auto k = _user_k;
	_nonlocal_radius[_qp] = _user_nonlocal_radius;
	auto strain = _strain[_qp];



    // Calculate the 1st Invariant I	
	ADReal I_1 = strain.trace();
	
	ADReal J_2 = (3 * (strain * strain).trace()) - (I_1 * I_1);
	
	
	
	// Calculate Equivalent Strain
	ADReal term1 = ((k-1.0)/((2.0*k)*(1.0-(2.0*nu))))*I_1;
	
	ADReal term2a =  ((k-1.0)*(k-1.0)*I_1*I_1)  / ((1.0-(2.0*nu)) * (1.0-(2.0*nu)));
	ADReal term2b = (2.0*k*J_2)/((1.0 + nu)*(1.0 + nu));
	
	ADReal term2 = (1.0/(2.0*k)) * pow((term2a + term2b),1.0/2.0);
	
	ADReal equiv_strain = term1 + term2;
	
	
	// Calculate Kappa: KKT Condition
	ADReal kappa = 0.0;
	
	equiv_strain = abs(equiv_strain);
	
	if (equiv_strain <= kappa_0)
	{	
      kappa = kappa_0;
	}
	else
	{
	  kappa = equiv_strain;
	}
	
	
	_kappa[_qp] = kappa;

	
	
	// Compute damage variable
	// Use nonlocal version to compute damage
	kappa = _kappa_bar[_qp];
	kappa = abs(kappa);
	
	if (kappa <= kappa_0)
	{	
      _D[_qp] = 0.0;
	}
	else
	{
	  _D[_qp] = 1.0 - (   (kappa_0/kappa) * ((1-alpha) + alpha*exp(-beta*(kappa - kappa_0)))  );
	}
	
}


