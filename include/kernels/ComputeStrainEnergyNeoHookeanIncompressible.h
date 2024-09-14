#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStrainEnergyNeoHookeanIncompressible : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ComputeStrainEnergyNeoHookeanIncompressible(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;
  
  /// Base name of the material system
  const std::string _base_name;

  /// Real valued constants from users
  const Real _user_mu_0;
  
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;

  MaterialProperty<Real> & _strain_energy;
  MaterialProperty<RankTwoTensor> & _dWdF;
};
