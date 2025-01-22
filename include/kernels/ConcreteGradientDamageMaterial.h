#pragma once

#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>
#include "ADMaterial.h"

class ConcreteGradientDamageMaterial : public DerivativeMaterialInterface<ADMaterial>
{
public:
  static InputParameters validParams();

  ConcreteGradientDamageMaterial(const InputParameters & parameters);

protected:

  virtual void computeQpProperties() override;

  /// Real valued constants from users
  const ADReal _user_nu;
  const ADReal _user_kappa_0;
  const ADReal _user_alpha;
  const ADReal _user_beta;
  const ADReal _user_k;
  const ADReal _user_nonlocal_radius;

  

  ADMaterialProperty<Real> & _nonlocal_radius;
  ADMaterialProperty<Real> & _D;
  ADMaterialProperty<Real> & _kappa;
  
  
  const ADMaterialProperty<RankTwoTensor> & _stress;
  const ADMaterialProperty<RankTwoTensor> & _strain;
  
  const ADVariableValue & _kappa_bar;
  
  ADMaterialProperty<Real> & _seeoutput;
  
  /// Number of dims
  unsigned n_dim;
};
