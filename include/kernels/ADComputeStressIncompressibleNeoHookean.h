#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ADComputeStressIncompressibleNeoHookean : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ADComputeStressIncompressibleNeoHookean(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override;
  
  ADRankTwoTensor computePiolaKStress2(const ADReal &mu, const ADRankTwoTensor &C, const ADRankTwoTensor &F, const ADReal &p);
  

  
  
  
  
  // Attributes
  const ADReal _user_mu;
  
  const ADVariableValue & _pressure;
  
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;

  ADMaterialProperty<RankTwoTensor> & _ad_cauchy_stress;
};
