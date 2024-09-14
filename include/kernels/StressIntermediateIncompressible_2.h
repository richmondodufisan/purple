#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class StressIntermediateIncompressible_2 : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  StressIntermediateIncompressible_2(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;
  
  /// Base name of the material system
  const std::string _base_name;

  const MaterialProperty<RankFourTensor> & _dPK1_dW_in;
  
  MaterialProperty<RankFourTensor> & _dPK1_dW_out;
};
