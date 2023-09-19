//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html
#include "purpleTestApp.h"
#include "purpleApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "MooseSyntax.h"

InputParameters
purpleTestApp::validParams()
{
  InputParameters params = purpleApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  return params;
}

purpleTestApp::purpleTestApp(InputParameters parameters) : MooseApp(parameters)
{
  purpleTestApp::registerAll(
      _factory, _action_factory, _syntax, getParam<bool>("allow_test_objects"));
}

purpleTestApp::~purpleTestApp() {}

void
purpleTestApp::registerAll(Factory & f, ActionFactory & af, Syntax & s, bool use_test_objs)
{
  purpleApp::registerAll(f, af, s);
  if (use_test_objs)
  {
    Registry::registerObjectsTo(f, {"purpleTestApp"});
    Registry::registerActionsTo(af, {"purpleTestApp"});
  }
}

void
purpleTestApp::registerApps()
{
  registerApp(purpleApp);
  registerApp(purpleTestApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
// External entry point for dynamic application loading
extern "C" void
purpleTestApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  purpleTestApp::registerAll(f, af, s);
}
extern "C" void
purpleTestApp__registerApps()
{
  purpleTestApp::registerApps();
}
