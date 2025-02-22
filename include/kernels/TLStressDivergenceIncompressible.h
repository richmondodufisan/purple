#pragma once

#include "Kernel.h"
#include "DerivativeMaterialInterface.h"

/**
 * Computes the divergence of 2.order stress tensors
 */

class TLStressDivergenceIncompressible : public DerivativeMaterialInterface<Kernel>
{
public:
  static InputParameters validParams();

  TLStressDivergenceIncompressible(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;

  Real computeQpJacobianDisplacement(unsigned int comp_i, unsigned int comp_k);

  /// Base name of the material system that this kernel applies to
  const std::string _base_name;



  /// The tensor
  const MaterialProperty<RankTwoTensor> & _P_hat;

  /// Derivatives of the w.r.t. strain increment
  const MaterialProperty<RankFourTensor> & _dP_hat_dF;
  
  /// The deformation gradient
  const MaterialProperty<RankTwoTensor> & _F;



  /// An integer corresponding to the direction this kernel acts in
  const unsigned int _component;

  /// Coupled displacement variables
  unsigned int _ndisp;
  /// Displacement variables IDs
  std::vector<unsigned int> _disp_var;




  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////

  /// Coupled pressure variable index
  const unsigned int _p_var;

  /// Coupled pressure field at quadrature points
  const VariableValue & _pressure;
  
  
  Real computeQpJacobianPressure(unsigned int comp_i);
  
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
};
