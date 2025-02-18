#pragma once

#include "ComputeLagrangianStressPK2.h"

class ComputeStressIncompressibleNeoHookean : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();
  ComputeStressIncompressibleNeoHookean(const InputParameters & parameters);

protected:
  /// Actual stress/Jacobian update
  virtual void computeQpPK2Stress();
  
  
  RankTwoTensor computePiolaKStress2(const Real &mu, const RankTwoTensor &C, const RankTwoTensor &F, const Real &p);
  RankFourTensor compute_dSdE(const Real &mu, const RankTwoTensor &C, const RankTwoTensor &F, const Real &p);

protected:
  const Real _user_mu;
  // const Real _user_kappa;
  
  const VariableValue & _pressure;
};
