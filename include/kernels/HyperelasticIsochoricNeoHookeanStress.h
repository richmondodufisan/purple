#pragma once

#include "ComputeLagrangianStressPK2.h"

class HyperelasticIsochoricNeoHookeanStress : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();
  HyperelasticIsochoricNeoHookeanStress(const InputParameters & parameters);

protected:
  /// Actual stress/Jacobian update
  virtual void computeQpPK2Stress();
  
  
  RankTwoTensor computePiolaKStress2(const Real &mu, const RankTwoTensor &C, const RankTwoTensor &F);
  RankFourTensor compute_dSdE(const Real &mu, const RankTwoTensor &C, const RankTwoTensor &F);

protected:
  const Real _user_mu;
};
