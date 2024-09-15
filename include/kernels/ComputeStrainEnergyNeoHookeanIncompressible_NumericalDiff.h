#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override;
  Real computeStrainEnergy(const Real &mu_0,const RankTwoTensor &F);
  RankTwoTensor computePiolaKStress1(const Real &W, const Real &mu_0, const RankTwoTensor &F, const RankTwoTensor &F_inv, const Real &p);
  RankTwoTensor compute_dWdF(const Real &mu_0, const RankTwoTensor &F);
  RankFourTensor compute_dPK1dF(const Real &W, const Real &mu_0, const RankTwoTensor &F, const RankTwoTensor &F_inv, const Real &p);

  
  
  
  
  // Attributes
  const std::string _base_name;
  const Real _user_mu_0;
  const VariableValue & _pressure;
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;
  const MaterialProperty<RankTwoTensor> & _deformation_gradient_inv;

  MaterialProperty<Real> & _strain_energy;
  MaterialProperty<RankTwoTensor> & _PK1;
  MaterialProperty<RankFourTensor> & _dPK1_dF;
};
