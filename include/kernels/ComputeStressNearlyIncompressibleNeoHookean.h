#pragma once

#include "ComputeLagrangianStressPK2.h"

class ComputeStressNearlyIncompressibleNeoHookean : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();
  ComputeStressNearlyIncompressibleNeoHookean(const InputParameters & parameters);

protected:
  /// Actual stress/Jacobian update
  virtual void computeQpPK2Stress();
  
  
  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &kappa, const RankTwoTensor &C, const RankTwoTensor &F);
  RankFourTensor compute_dSdE(const Real &mu, const Real &kappa, const RankTwoTensor &C, const RankTwoTensor &F);

protected:
  const Real _user_mu;
  
  const Real _user_kappa;
};
