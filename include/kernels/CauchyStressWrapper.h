#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class CauchyStressWrapper : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  CauchyStressWrapper(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override; 
  virtual void initQpStatefulProperties() override;
  
  
  // Attributes
  const std::string _base_name;
  const MaterialProperty<RankTwoTensor> & _cauchy_stress_in;
  const MaterialProperty<RankFourTensor> & _cauchy_jacobian_in;

  MaterialProperty<RankTwoTensor> & _stress;
  MaterialProperty<RankFourTensor> & _Jacobian_mult;
};
