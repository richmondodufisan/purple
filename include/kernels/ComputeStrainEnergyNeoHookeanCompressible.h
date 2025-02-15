#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStrainEnergyNeoHookeanCompressible : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ComputeStrainEnergyNeoHookeanCompressible(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override;
  Real computeStrainEnergy(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  RankTwoTensor compute_dWdC(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  RankFourTensor compute_dPK2dE(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  
  Real chooseOptimalEpsilon(const Real &value);
  // void setNearZeroToZero(RankTwoTensor &tensor, const Real tolerance);
  

  
  
  
  
  // Attributes
  const std::string _base_name;
  
  const Real _user_mu;
  const Real _user_lambda;
  
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;

  MaterialProperty<Real> & _strain_energy;
  MaterialProperty<RankTwoTensor> & _PK2;
  MaterialProperty<RankFourTensor> & _dPK2_dE;
};
