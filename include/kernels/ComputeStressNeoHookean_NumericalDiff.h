#pragma once

#include "ComputeLagrangianStressPK1.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStressNeoHookean_NumericalDiff : public ComputeLagrangianStressPK1
{
public:
  static InputParameters validParams();

  ComputeStressNeoHookean_NumericalDiff(const InputParameters & parameters);

protected:

  virtual void computeQpPK1Stress() override;
  
  /// Base name of the material system
  const std::string _base_name;
  
  // for getting them
  const MaterialProperty<RankTwoTensor> & _PK1_in;
  const MaterialProperty<RankFourTensor> & _dPdF_in;
};
