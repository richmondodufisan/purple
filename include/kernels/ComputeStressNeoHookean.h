#pragma once

#include "ComputeLagrangianStressPK2.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ComputeStressNeoHookean : public ComputeLagrangianStressPK2
{
public:
  static InputParameters validParams();

  ComputeStressNeoHookean(const InputParameters & parameters);

protected:

  virtual void computeQpPK2Stress() override;
  
  // Base name of the material system
  const std::string _base_name;
  
  // for getting them
  const MaterialProperty<RankTwoTensor> & _PK2_in;
  const MaterialProperty<RankFourTensor> & _dPdE_in;
};
