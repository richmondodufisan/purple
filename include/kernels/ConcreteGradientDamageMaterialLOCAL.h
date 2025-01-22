#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ConcreteGradientDamageMaterialLOCAL : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ConcreteGradientDamageMaterialLOCAL(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;

  /// Real valued constants from users
  const ADReal _user_nu;
  const ADReal _user_kappa_0;
  const ADReal _user_alpha;
  const ADReal _user_beta;
  const ADReal _user_k;

  

  ADMaterialProperty<Real> & _D;
  
  
  const ADMaterialProperty<RankTwoTensor> & _stress;
  const ADMaterialProperty<RankTwoTensor> & _strain;

  
  ADMaterialProperty<Real> & _seeoutput;
  
  /// Number of dims
  unsigned n_dim;
};
