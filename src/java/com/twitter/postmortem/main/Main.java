package com.twitter.postmortem.main;

import java.net.InetSocketAddress;
import java.util.Arrays;

import com.google.common.collect.ImmutableMap;
import com.google.inject.AbstractModule;
import com.google.inject.Inject;
import com.google.inject.Module;
import com.google.inject.TypeLiteral;
import com.sun.jersey.guice.JerseyServletModule;
import com.sun.jersey.guice.spi.container.servlet.GuiceContainer;

import com.twitter.common.application.AbstractApplication;
import com.twitter.common.application.AppLauncher;
import com.twitter.common.application.Lifecycle;
import com.twitter.common.application.http.Registration;
import com.twitter.common.application.modules.HttpModule;
import com.twitter.common.application.modules.LogModule;
import com.twitter.common.application.modules.StatsModule;
import com.twitter.common.args.Arg;
import com.twitter.common.args.CmdLine;
import com.twitter.common.args.constraints.NotNull;
import com.twitter.common.base.Closure;
import com.twitter.postmortem.handler.ReadHandler;
import com.twitter.postmortem.handler.WriteHandler;

/**
 *
 */
public class Main extends AbstractApplication {
  @Inject private Lifecycle lifecycle;

  @Override
  public void run() {
    lifecycle.awaitShutdown();
  }

  @Override
  public Iterable<? extends Module> getModules() {
    return Arrays.asList(
        new HttpModule(),
        new LogModule(),
        new StatsModule(),
        new AbstractModule() {
          @Override protected void configure() {
            install(new JerseyServletModule() {
              @Override protected void configureServlets() {
                filter("/write*").through(
                    GuiceContainer.class, ImmutableMap.<String, String>of());
                filter("/read*").through(
                    GuiceContainer.class, ImmutableMap.<String, String>of());
                Registration.registerEndpoint(binder(), "/write");
                Registration.registerEndpoint(binder(), "/read");
                bind(ReadHandler.class);
                bind(WriteHandler.class);
              }
            });
          }
        }
    );
  }

  public static void main(String[] args) {
    AppLauncher.launch(Main.class, args);
  }
}
