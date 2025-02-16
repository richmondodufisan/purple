#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStressCompressibleNeoHookean2 : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ComputeStressCompressibleNeoHookean2(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override;

  
  // Base name of the material system
  const std::string _base_name;
 

  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  RankFourTensor compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  
  RankFourTensor innerProduct4thOrder(const RankFourTensor &A, const RankFourTensor &B);
  RankFourTensor kroneckerProduct4thOrder(const RankTwoTensor &A, const RankTwoTensor &B);
  
  
  
  const Real _user_mu;
  const Real _user_lambda;
  
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;
  
  
  MaterialProperty<RankTwoTensor> & _PK2;
  MaterialProperty<RankFourTensor> & _dPK2_dE;
};
