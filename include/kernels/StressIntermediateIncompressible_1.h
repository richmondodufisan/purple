#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class StressIntermediateIncompressible_1 : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  StressIntermediateIncompressible_1(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;
  
  /// Base name of the material system
  const std::string _base_name;

  const MaterialProperty<RankTwoTensor> & _dWdF;
  const MaterialProperty<RankTwoTensor> & _deformation_gradient;
  
  const VariableValue & _pressure;
  
  MaterialProperty<RankTwoTensor> & _dWdF_pF_out;
  MaterialProperty<RankFourTensor> & _tangent_out;
};
