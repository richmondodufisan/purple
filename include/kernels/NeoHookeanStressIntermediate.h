#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class NeoHookeanStressIntermediate : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  NeoHookeanStressIntermediate(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;
  
  /// Base name of the material system
  const std::string _base_name;

  const MaterialProperty<RankTwoTensor> & _dWdF;
  const MaterialProperty<RankFourTensor> & _d2WdF2;
  
  MaterialProperty<RankTwoTensor> & _dWdF_out;
  MaterialProperty<RankFourTensor> & _d2WdF2_out;
};
