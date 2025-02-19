#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ADCauchyStressWrapper : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ADCauchyStressWrapper(const InputParameters & parameters);

protected:

  // Methods
  virtual void computeQpProperties() override; 
  virtual void initQpStatefulProperties() override;
  
  
  // Attributes
  const std::string _base_name;
  const ADMaterialProperty<RankTwoTensor> & _cauchy_stress_in;

  ADMaterialProperty<RankTwoTensor> & _stress;
};
