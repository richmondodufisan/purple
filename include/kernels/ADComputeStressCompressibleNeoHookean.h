#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ADComputeStressCompressibleNeoHookean : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ADComputeStressCompressibleNeoHookean(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;


  ADRankTwoTensor computePiolaKStress2(const ADReal &mu, const ADReal &lambda, const ADRankTwoTensor &C_inv, const ADRankTwoTensor &F);
  ADRankFourTensor compute_dSdE(const ADReal &mu, const ADReal &lambda, const ADRankTwoTensor &C_inv, const ADRankTwoTensor &F);


  /// Prepend to the material properties
  const std::string _base_name;


  // Real valued constants from users
  const ADReal _user_lambda;
  const ADReal _user_mu;
  

  const ADMaterialProperty<RankTwoTensor> & _deformation_gradient;
  
  
  
  
  ADMaterialProperty<RankTwoTensor> & _stress;
};
