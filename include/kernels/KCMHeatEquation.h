#pragma once

#include "ADKernel.h"
#include <cmath>
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class KCMHeatEquation : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    KCMHeatEquation(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    // Base name of the material system that this kernel applies to if needed
    const std::string _base_name;

    // Parameters
    const unsigned int _component_flux;
	
	const ADVariableGradient & _grad_temp;
	
	const ADVariableValue & _q_x;
	const ADVariableValue & _q_y;
	const ADVariableValue & _q_z;
	
	const ADVariableGradient & _grad_q_x;
	const ADVariableGradient & _grad_q_y;
	const ADVariableGradient & _grad_q_z;
	
	const ADMaterialProperty<Real> & _kappa;
	const ADMaterialProperty<Real> & _length_scale;
	const ADMaterialProperty<Real> & _alpha;
};
