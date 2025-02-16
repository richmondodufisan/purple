#pragma once

#include "ComputeLagrangianStressPK2.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStressCompressibleNeoHookean : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();

  ComputeStressCompressibleNeoHookean(const InputParameters & parameters);

protected:

  virtual void computeQpPK2Stress() override;
  
  // Base name of the material system
  const std::string _base_name;
 

  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  RankFourTensor compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C);
  
  RankFourTensor innerProduct4thOrder(const RankFourTensor &A, const RankFourTensor &B);
  RankFourTensor kroneckerProduct4thOrder(const RankTwoTensor &A, const RankTwoTensor &B);
  
  
  
  const Real _user_mu;
  const Real _user_lambda;
};
