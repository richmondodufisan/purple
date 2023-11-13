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

class DiffusionTemperature : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    DiffusionTemperature(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    // Base name of the material system that this kernel applies to if needed
    const std::string _base_name;

    // Parameters	
	const ADVariableValue & _q_x;
	const ADVariableValue & _q_y;
	const ADVariableValue & _q_z;
};
