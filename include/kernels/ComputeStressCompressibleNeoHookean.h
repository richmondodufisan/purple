#pragma once

#include "ComputeLagrangianStressPK2.h"

class ComputeStressCompressibleNeoHookean : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();
  ComputeStressCompressibleNeoHookean(const InputParameters & parameters);

protected:
  /// Actual stress/Jacobian update
  virtual void computeQpPK2Stress();
  
  
  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C, const RankTwoTensor &F);
  RankFourTensor compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C, const RankTwoTensor &F);
  
  RankFourTensor innerProduct4thOrder(const RankFourTensor &A, const RankFourTensor &B);
  RankFourTensor kroneckerProduct4thOrder(const RankTwoTensor &A, const RankTwoTensor &B);

protected:
  const Real _user_mu;
  const Real _user_lambda;
};
