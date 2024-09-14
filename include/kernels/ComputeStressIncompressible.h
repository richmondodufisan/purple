#pragma once

#include "ComputeLagrangianStressPK1.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStressIncompressible : public ComputeLagrangianStressPK1
{
public:
  static InputParameters validParams();

  ComputeStressIncompressible(const InputParameters & parameters);

protected:

  virtual void computeQpPK1Stress() override;
  
  /// Base name of the material system
  const std::string _base_name;
  
  // for getting them
  const MaterialProperty<RankTwoTensor> & _dWdF_pF_in;
  const MaterialProperty<RankFourTensor> & _dPK1_dW_in;
};
