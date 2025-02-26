#pragma once

#include "ComputeLagrangianStressPK2.h"

class HyperelasticNeoHookeanStress : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();
  HyperelasticNeoHookeanStress(const InputParameters & parameters);

protected:
  /// Actual stress/Jacobian update
  virtual void computeQpPK2Stress();
  
  
  RankTwoTensor computePiolaKStress2(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F);
  RankFourTensor compute_dSdE(const Real &mu, const Real &lambda, const RankTwoTensor &C_inv, const RankTwoTensor &F);

protected:
  const Real _user_mu;
  const Real _user_lambda;
};
