#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff_PK2 : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ComputeStrainEnergyNeoHookeanIncompressible_NumericalDiff_PK2(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override;
  Real computeStrainEnergy(const Real &mu_0, const RankTwoTensor &C);
  RankTwoTensor compute_dWdC(const Real &mu_0, const RankTwoTensor &C);
  RankTwoTensor computePiolaKStress2(const Real &mu_0, const RankTwoTensor &E, const Real &p);
  RankFourTensor compute_dPK2dE(const Real &mu_0, const RankTwoTensor &E, const Real &p);
  
  void setNearZeroToZero(RankTwoTensor &tensor, const Real tolerance);

  
  
  
  
  // Attributes
  const std::string _base_name;
  const Real _user_mu_0;
  const VariableValue & _pressure;
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;

  MaterialProperty<Real> & _strain_energy;
  MaterialProperty<RankTwoTensor> & _PK2;
  MaterialProperty<RankFourTensor> & _dPK2_dE;
};
