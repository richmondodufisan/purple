#pragma once

#include "IntegratedBC.h"

// class Function;

// /**
 // * Boundary condition of a Neumann style whose value is computed by a user-defined function
 // */
 
class RingGaussianPumpBessel : public IntegratedBC
{
public:
  static InputParameters validParams();

  RingGaussianPumpBessel(const InputParameters & parameters);

protected:
  virtual Real computeQpResidual() override;

  /// The function being used for setting the value
  // const Function & _func;
  
  const Real _pump_power;
  const Real _absorbance;
  const Real _pump_spot_size;
  
  const Real _center_x;
  const Real _center_y;
};
