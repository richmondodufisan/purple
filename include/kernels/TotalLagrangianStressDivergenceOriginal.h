#pragma once

#include "Kernel.h"
#include "DerivativeMaterialInterface.h"
#include "JvarMapInterface.h"

/// Base class of the "Lagrangian" kernel system
///
/// This class provides a common structure for the "new" tensor_mechanics
/// kernel system.  The goals for this new system are
///   1) Always-correct jacobians
///   2) A cleaner material interface
///
/// This class provides common input properties and helper methods,
/// most of the math has to be done in the subclasses
///
class TotalLagrangianStressDivergenceOriginal
  : public JvarMapKernelInterface<DerivativeMaterialInterface<Kernel>>
{
public:
  static InputParameters validParams();
  TotalLagrangianStressDivergenceOriginal(const InputParameters & parameters);

protected:

  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;
  
  
  
  virtual void initialSetup() override;



protected:
  /// If true use large deformation kinematics
  const bool _large_kinematics;

  /// Prepend to the material properties
  const std::string _base_name;

  /// Which component of the vector residual this kernel is responsible for
  const unsigned int _alpha;

  /// Total number of displacements/size of residual vector
  const unsigned int _ndisp;

  /// The displacement numbers
  std::vector<unsigned int> _disp_nums;

  // Averaged trial function gradients for each displacement component
  // i.e. _avg_grad_trial[a][j] returns the average gradient of trial function associated with
  // node j with respect to displacement component a.
  std::vector<std::vector<RankTwoTensor>> _avg_grad_trial;

  /// The unmodified deformation gradient
  const MaterialProperty<RankTwoTensor> & _F_ust;

  /// The element-average deformation gradient
  const MaterialProperty<RankTwoTensor> & _F_avg;

  /// The inverse increment deformation gradient
  const MaterialProperty<RankTwoTensor> & _f_inv;

  /// The inverse deformation gradient
  const MaterialProperty<RankTwoTensor> & _F_inv;

  /// The actual (stabilized) deformation gradient
  const MaterialProperty<RankTwoTensor> & _F;
  
  /// The 1st Piola-Kirchhoff stress
  const MaterialProperty<RankTwoTensor> & _pk1;

  /// The derivative of the PK1 stress with respect to the
  /// deformation gradient
  const MaterialProperty<RankFourTensor> & _dpk1;
  
  
  
  
  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  // // Material parameter (shear modulus)
  // const Real _mu;

  // /// Coupled pressure variable index
  // const unsigned int _p_var;

  // /// Coupled pressure field at quadrature points
  // const VariableValue & _p;
  
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
};
